import { useState, useEffect } from 'react';
import { AuthUser } from '../types';
import { 
    signInWithPopup, 
    GoogleAuthProvider, 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword,
    updateProfile,
    signOut as firebaseSignOut, 
    onAuthStateChanged, 
    User 
} from 'firebase/auth';
import { auth, db, handleFirestoreError, OperationType } from '../firebase';
import { doc, setDoc, getDoc, getDocFromServer } from 'firebase/firestore';

const googleProvider = new GoogleAuthProvider();

// Mapper from Firebase User to our AuthUser
const mapFirebaseUser = (user: User, overrideType?: 'applicant' | 'mentor' | 'university'): AuthUser => {
    return {
        id: user.uid,
        name: user.displayName || 'User',
        email: user.email || '',
        emailVerified: user.emailVerified,
        image: user.photoURL || undefined,
        createdAt: new Date(user.metadata.creationTime || Date.now()),
        updatedAt: new Date(user.metadata.lastSignInTime || Date.now()),
        type: overrideType || 'applicant'
    };
};

export const authClient = {
  signIn: {
    social: async ({ provider, role = 'applicant' }: { provider: 'google' | 'github', role?: 'applicant' | 'mentor' | 'university' }) => {
        if (provider === 'google') {
             try {
                console.log("Initiating Google Sign-In with role:", role);
                const result = await signInWithPopup(auth, googleProvider);
                console.log("Google Sign-In successful for UID:", result.user.uid);
                localStorage.setItem('gradwyn_user_role', role);
                
                // Ensure user document exists in Firestore
                const userDocRef = doc(db, 'users', result.user.uid);
                let userDoc;
                try {
                    userDoc = await getDocFromServer(userDocRef);
                } catch (e) {
                    userDoc = await getDoc(userDocRef);
                }
                
                if (!userDoc.exists()) {
                    console.log("Creating new user document in Firestore...");
                    try {
                        await setDoc(userDocRef, {
                            id: result.user.uid,
                            email: result.user.email,
                            name: result.user.displayName || 'User',
                            role: role,
                            createdAt: new Date().toISOString()
                        });
                    } catch (error) {
                        handleFirestoreError(error, OperationType.WRITE, `users/${result.user.uid}`);
                    }
                }
                
                return { data: mapFirebaseUser(result.user, role), error: null };
             } catch (error: any) {
                console.error("Google Sign-In Error:", error);
                if (error.code === 'auth/popup-closed-by-user') return { data: null, error: "Sign-in cancelled." };
                if (error.code === 'auth/account-exists-with-different-credential') return { data: null, error: "An account already exists with the same email address but different sign-in credentials." };
                if (error.code === 'auth/unauthorized-domain') {
                    return { data: null, error: "This domain is not authorized for Firebase Authentication. Please add " + window.location.hostname + " to the 'Authorized domains' list in your Firebase Console (Authentication > Settings)." };
                }
                return { data: null, error: `Authentication failed: ${error.message} (${error.code})` };
             }
        }
        return { data: null, error: "Provider not supported" };
    },
    
    signUpEmail: async ({ email, password, name, role }: { email: string, password: string, name: string, role: 'applicant' | 'mentor' | 'university' }) => {
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            await updateProfile(userCredential.user, { displayName: name });
            localStorage.setItem('gradwyn_user_role', role);
            
            // Create user document in Firestore
            try {
                await setDoc(doc(db, 'users', userCredential.user.uid), {
                    id: userCredential.user.uid,
                    email: email,
                    name: name,
                    role: role,
                    createdAt: new Date().toISOString()
                });
            } catch (error) {
                handleFirestoreError(error, OperationType.WRITE, `users/${userCredential.user.uid}`);
            }
            
            return { data: mapFirebaseUser(userCredential.user, role), error: null };
        } catch (error: any) {
            console.error("signUpEmail error:", error);
            if (error.code === 'auth/email-already-in-use') {
                return { data: null, error: "This email is already in use. If you signed up with Google previously, please use 'Continue with Google' to log in." };
            }
            if (error.code === 'auth/weak-password') {
                return { data: null, error: "Password should be at least 6 characters." };
            }
            return { data: null, error: error.message };
        }
    },

    signInEmail: async ({ email, password }: { email: string, password: string }) => {
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const storedRole = localStorage.getItem('gradwyn_user_role') as 'applicant' | 'mentor' | 'university' | null;
            return { data: mapFirebaseUser(userCredential.user, storedRole || 'applicant'), error: null };
        } catch (error: any) {
            console.error("signInEmail error:", error);
            if (error.code === 'auth/invalid-credential') {
                return { data: null, error: "Invalid email or password. If you signed up with Google, please use 'Continue with Google'." };
            }
            return { data: null, error: error.message };
        }
    }
  },
  
  signOut: async () => {
     try {
        await firebaseSignOut(auth);
        return { data: true, error: null };
     } catch (error: any) {
        return { data: null, error: error.message };
     }
  },

  deleteAccount: async () => {
    try {
        const user = auth.currentUser;
        if (!user) throw new Error("No authenticated user found.");
        
        await user.delete();
        return { data: true, error: null };
    } catch (error: any) {
        console.error("deleteAccount error:", error);
        return { data: null, error: error.message };
    }
  },
  
  useSession: () => {
    const [data, setData] = useState<AuthUser | null>(null);
    const [isPending, setIsPending] = useState(true);
    const [error, setError] = useState<any>(null);

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (user) {
                const storedRole = localStorage.getItem('gradwyn_user_role') as 'applicant' | 'mentor' | 'university' | null;
                setData(mapFirebaseUser(user, storedRole || 'applicant'));
            } else {
                setData(null);
            }
            setIsPending(false);
        }, (err) => {
            setData(null);
            setError(err);
            setIsPending(false);
        });

        return () => unsubscribe();
    }, []);

    return { data, isPending, error };
  }
};