Since your **login page** is built using **React** and integrated into **Astro** via **@astro/react**, here’s how you can implement authentication with middleware in **Astro.js** while leveraging the **React login page**.

---

## **1. React Login Page**

### **`src/components/Login.jsx`**

```jsx
import { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include', // Includes HTTP-only cookies
      });

      const data = await response.json();

      if (response.ok) {
        window.location.href = '/dashboard'; // Redirect on successful login
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
```

---

## **2. Astro Page with React Component**

### **`src/pages/login.astro`**

```astro
---
import Login from '../components/Login.jsx';
---

<html lang="en">
  <head>
    <title>Login</title>
  </head>
  <body>
    <h1>Login Page</h1>
    <Login />
  </body>
</html>
```

---

## **3. API Endpoint for Authentication**

### **`src/pages/api/login.ts`**

```typescript
import type { APIRoute } from 'astro';
import jwt from 'jsonwebtoken';
import { serialize } from 'cookie';

export const post: APIRoute = async ({ request }) => {
  const { email, password } = await request.json();

  // Replace this with real authentication logic
  const user = await authenticateUser(email, password);

  if (!user) {
    return new Response(
      JSON.stringify({ error: 'Invalid credentials' }),
      {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }

  // Generate JWT token
  const token = jwt.sign(
    { userId: user.id, email: user.email },
    import.meta.env.JWT_SECRET,
    { expiresIn: '1h' }
  );

  // Set token in an HTTP-only cookie
  const cookie = serialize('accessToken', token, {
    httpOnly: true,
    secure: import.meta.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60, // 1 hour
  });

  return new Response(
    JSON.stringify({ message: 'Login successful' }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Set-Cookie': cookie,
      },
    }
  );
};

// Mock authentication
async function authenticateUser(email: string, password: string) {
  if (email === 'test@example.com' && password === 'password') {
    return { id: 1, email };
  }
  return null;
}
```

---

## **4. Middleware for Authentication**

### **`src/middleware.ts`**

```typescript
import type { MiddlewareHandler } from 'astro';
import jwt from 'jsonwebtoken';
import { parse } from 'cookie';

export const onRequest: MiddlewareHandler = async ({ request, locals }, next) => {
  const cookieHeader = request.headers.get('cookie') || '';
  const cookies = parse(cookieHeader);
  const token = cookies.accessToken;

  if (token) {
    try {
      const decoded = jwt.verify(token, import.meta.env.JWT_SECRET) as { userId: number; email: string };

      // Attach user info to locals
      locals.user = {
        id: decoded.userId,
        email: decoded.email,
      };
    } catch (err) {
      console.error('Invalid token:', err);
    }
  }

  // Proceed with the request
  return await next();
};
```

### **Type Declaration**

Add type declaration for `locals`.

**`src/types/astro.d.ts`**

```typescript
declare namespace App {
  interface Locals {
    user?: {
      id: number;
      email: string;
    };
  }
}
```

---

## **5. Protect Routes (e.g., Dashboard)**

### **`src/pages/dashboard.astro`**

```astro
---
const { user } = Astro.locals;

if (!user) {
  return Astro.redirect('/login');
}
---

<html lang="en">
  <head>
    <title>Dashboard</title>
  </head>
  <body>
    <h1>Welcome, {user.email}!</h1>
    <p>This is your dashboard.</p>
    <a href="/api/logout">Logout</a>
  </body>
</html>
```

---

## **6. Logout Functionality**

### **`src/pages/api/logout.ts`**

```typescript
import type { APIRoute } from 'astro';
import { serialize } from 'cookie';

export const post: APIRoute = async () => {
  const cookie = serialize('accessToken', '', {
    httpOnly: true,
    secure: import.meta.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    expires: new Date(0), // Immediately expire
  });

  return new Response(
    JSON.stringify({ message: 'Logged out successfully' }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Set-Cookie': cookie,
      },
    }
  );
};
```

**React Logout Button:**

```jsx
const Logout = () => {
  const handleLogout = async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include',
    });
    window.location.href = '/login';
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default Logout;
```

---

## **7. Security Best Practices**

1. **Environment Variables:**
   Add this to `.env`:
   ```
   JWT_SECRET=your_jwt_secret
   ```

2. **Use HTTPS in Production:**
   Ensure `secure: true` for cookies when deploying in production.

3. **Rate Limiting:**
   Prevent brute-force attacks on the login endpoint by implementing rate limiting.

4. **Token Refresh Logic:**
   Add token refresh and expiration handling for smoother sessions.

---

### **Summary**

This implementation:

- Uses **React** for the login form.
- Utilizes Astro's **API routes** for authentication.
- Leverages **Astro middleware** to validate tokens and inject user info into requests.
- Provides route protection (e.g., dashboard).
- Implements logout functionality.

Let me know if you need additional assistance!