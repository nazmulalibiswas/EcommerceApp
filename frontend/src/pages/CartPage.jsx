import { useCart } from '../context/CartContext.jsx';
import { Link } from "react-router-dom";

function CartPage() {
  const { cartItems, total, removeFromCart, updateQuantity } = useCart();
  const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL || "http://127.0.0.1:8000";
  console.log("Cart Items: ", cartItems);

  return (
    <div className="pt-20 min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6 text-center">Your Cart</h1>
      {cartItems.length === 0 ? (
        <p className="text-center text-gray-600">Your cart is empty</p>
      ) : (
        <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
          {cartItems.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between mb-4 border-b pb-4"
            >
              <div className="flex items-center gap-4">
                {item.product_image && (
                  <img 
                    src={
                      item.product_image.startsWith("http")
                        ? item.product_image
                        : item.product_image.startsWith("/media/")
                        ? `${BASEURL}${item.product_image}`
                        : item.product_image.startsWith("/")
                        ? `${BASEURL}${item.product_image}`
                        : `${BASEURL}/media/${item.product_image}`
                    } 
                    alt={item.product_name}
                    className="w-20 h-20 object-cover rounded"
                    onError={(e) => {
                      // ইমেজ লোড না হলে ভাঙা আইকন হাইড করে দেবো
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                <div>
                  <h2 className="text-lg font-semibold">
                    {item.product_name || item.product?.name || item.name}
                  </h2>
                  <p className="text-gray-600">
                    ${item.product_price || item.product?.price || item.price}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  className="bg-gray-300 px-3 py-1 rounded"
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                >
                  -
                </button>
                <span>{item.quantity}</span>
                <button
                  className="bg-gray-300 px-3 py-1 rounded"
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                >
                  +
                </button>
                <button
                  className="text-red-500"
                  onClick={() => removeFromCart(item.id)}
                >
                  Remove
                </button>
              </div>
            </div>
          ))}

          <div className="border-t pt-4 mt-4 flex justify-between items-center">
            <h2 className="text-xl font-bold">Total:</h2>
            <p className="text-xl font-semibold">${Number(total).toFixed(2)}</p>
            <Link to="/checkout" className="bg-blue-600 text-white px-6 py-2 rounded-lg duration-300">
              Proceed to Checkout
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default CartPage;