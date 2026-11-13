import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProductList from "./pages/ProductList";
import ProductDetails from "./pages/ProductDetails";
import Navbar from "./components/Navbar";
import CartPage from "./pages/CartPage";
import { CartProvider } from "./context/CartContext"; // Use "./" if context is inside src/, or "../" if outside src/
import CheckoutPage from "./pages/CheckoutPage";
import PrivateRouter from './components/PrivateRouter';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <CartProvider>
      <Router>
        <Navbar />
        <div className="pt-16">
          <Routes>
            <Route path="/" element={<ProductList/>}/>
            <Route path="/product/:id" element={<ProductDetails/>}/>
            <Route path="/cart" element={<CartPage/>}/>
            <Route element={<PrivateRouter/>}>
              <Route path="/checkout" element={<CheckoutPage/>}/>
            </Route>
            <Route path="/login" element={<Login/>}/>
            <Route path="/signup" element={<Signup/>}/>
          </Routes>
        </div>
      </Router>
    </CartProvider>
  );
}

export default App;