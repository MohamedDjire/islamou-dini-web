import { lazy, Suspense } from 'react'
import { createBrowserRouter, Navigate } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'
import AuthLayout from '../layouts/AuthLayout'
import { PageLoader } from '../components/ui/Loader'

// Lazy loading des pages
const HomePage = lazy(() => import('../pages/HomePage'))
const DashboardPage = lazy(() => import('../pages/DashboardPage'))
const LoginPage = lazy(() => import('../pages/auth/LoginPage'))
const RegisterPage = lazy(() => import('../pages/auth/RegisterPage'))
const ForgotPasswordPage = lazy(() => import('../pages/auth/ForgotPasswordPage'))
const FormationsPage = lazy(() => import('../pages/formations/FormationsPage'))
const FormationDetailPage = lazy(() => import('../pages/formations/FormationDetailPage'))
const FormationPlayerPage = lazy(() => import('../pages/formations/FormationPlayerPage'))
const ReelsPage = lazy(() => import('../pages/reels/ReelsPage'))
const CommunitiesPage = lazy(() => import('../pages/communities/CommunitiesPage'))
const CommunityDetailPage = lazy(() => import('../pages/communities/CommunityDetailPage'))
const LivesPage = lazy(() => import('../pages/lives/LivesPage'))
const MessagesPage = lazy(() => import('../pages/messages/MessagesPage'))
const ProfilePage = lazy(() => import('../pages/profile/ProfilePage'))
const SearchPage = lazy(() => import('../pages/search/SearchPage'))
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'))

// Wrapper pour Suspense
const SuspenseWrapper = ({ children }) => (
  <Suspense fallback={<PageLoader />}>
    {children}
  </Suspense>
)

// Composant pour les routes protegees
import { useAuth } from '../context/AuthContext'

function PrivateRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <PageLoader />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

// Configuration du router
export const router = createBrowserRouter([
  // Landing page publique
  {
    path: '/',
    element: (
      <SuspenseWrapper>
        <HomePage />
      </SuspenseWrapper>
    ),
  },
  // Routes d'authentification
  {
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: (
          <SuspenseWrapper>
            <LoginPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'register',
        element: (
          <SuspenseWrapper>
            <RegisterPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'forgot-password',
        element: (
          <SuspenseWrapper>
            <ForgotPasswordPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  // Routes principales (avec layout)
  {
    element: <MainLayout />,
    children: [
      {
        path: 'dashboard',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <DashboardPage />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      // Formations
      {
        path: 'formations',
        element: (
          <SuspenseWrapper>
            <FormationsPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'formations/:id',
        element: (
          <SuspenseWrapper>
            <FormationDetailPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'formations/:id/learn',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <FormationPlayerPage />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      {
        path: 'my-formations',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <FormationsPage isMyFormations />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      // Reels
      {
        path: 'reels',
        element: (
          <SuspenseWrapper>
            <ReelsPage />
          </SuspenseWrapper>
        ),
      },
      // Communautes
      {
        path: 'communities',
        element: (
          <SuspenseWrapper>
            <CommunitiesPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'communities/:id',
        element: (
          <SuspenseWrapper>
            <CommunityDetailPage />
          </SuspenseWrapper>
        ),
      },
      // Lives
      {
        path: 'lives',
        element: (
          <SuspenseWrapper>
            <LivesPage />
          </SuspenseWrapper>
        ),
      },
      // Messages
      {
        path: 'messages',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <MessagesPage />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      {
        path: 'messages/:conversationId',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <MessagesPage />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      // Profil
      {
        path: 'profile',
        element: (
          <PrivateRoute>
            <SuspenseWrapper>
              <ProfilePage />
            </SuspenseWrapper>
          </PrivateRoute>
        ),
      },
      {
        path: 'users/:id',
        element: (
          <SuspenseWrapper>
            <ProfilePage isPublic />
          </SuspenseWrapper>
        ),
      },
      // Recherche
      {
        path: 'search',
        element: (
          <SuspenseWrapper>
            <SearchPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  // 404
  {
    path: '*',
    element: (
      <SuspenseWrapper>
        <NotFoundPage />
      </SuspenseWrapper>
    ),
  },
])

export default router
