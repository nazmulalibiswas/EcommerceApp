import { createContext, useContext, useState, useEffect } from "react";
import { authFetch } from "../utils/auth";

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const rawBaseUrl =
    import.meta.env.VITE_DJANGO_BASE_URL ||
    import.meta.env.VITE_BASE_URL ||
    "http://127.0.0.1:8000";
  const BASEURL = rawBaseUrl.replace(/\/$/, "");

  const [cartItems, setCartItems] = useState([]);
  const [total, setTotal] = useState(0);

  // Fetch Cart from BE
  const fetchCart = async () => {
    try {
      const res = await authFetch(`${BASEURL}/api/cart/`);
      if (res.ok) {
        const data = await res.json();
        setCartItems(data.items || []);
        setTotal(data.total || 0);
      }
    } catch (error) {
      console.error("Error fetching cart: ", error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  // Add Product to Cart (Supports both addToCart(product.id) and addToCart(product))
  const addToCart = async (productOrId) => {
    const productId =
      typeof productOrId === "object" && productOrId !== null
        ? productOrId.id
        : productOrId;

    try {
      const res = await authFetch(`${BASEURL}/api/cart/add/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      });

      if (res.ok) {
        await fetchCart();
      } else {
        const err = await res.json().catch(() => ({}));
        console.error("Failed to add to cart:", err);
      }
    } catch (error) {
      console.error("Error adding to cart: ", error);
    }
  };

  // Remove Product from Cart
  const removeFromCart = async (itemId) => {
    try {
      const res = await authFetch(`${BASEURL}/api/cart/remove/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ item_id: itemId }),
      });

      if (res.ok) {
        await fetchCart();
      }
    } catch (error) {
      console.error("Error removing from cart: ", error);
    }
  };

  // Update Quantity
  const updateQuantity = async (itemId, quantity) => {
    if (quantity < 1) {
      await removeFromCart(itemId);
      return;
    }

    try {
      const res = await authFetch(`${BASEURL}/api/cart/update/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ item_id: itemId, quantity }),
      });

      if (res.ok) {
        await fetchCart();
      }
    } catch (error) {
      console.error("Failed to update cart quantity:", error);
    }
  };

  const clearCart = () => {
    setCartItems([]);
    setTotal(0);
  };

  return (
    <CartContext.Provider
      value={{
        cartItems,
        total,
        fetchCart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  return useContext(CartContext);
};