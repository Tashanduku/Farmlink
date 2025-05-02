// src/components/common/Layout.jsx
// components/common/Layout.jsx
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div>
      <header>
        {/* You can add a navigation bar here */}
        <nav>
          {/* Add navigation links if necessary */}
        </nav>
      </header>
      <main>
        <Outlet /> {/* This renders the nested routes like Profile */}
      </main>
    </div>
  );
};

export default Layout;
