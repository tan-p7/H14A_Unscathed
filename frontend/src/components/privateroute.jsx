import { Navigate } from 'react-router-dom'
import { isLoggedIn } from '../api/auth'

function PrivateRoute({ children }) {
  if (!isLoggedIn()) {
    return <Navigate to="/" />
  }
  return children
}

export default PrivateRoute