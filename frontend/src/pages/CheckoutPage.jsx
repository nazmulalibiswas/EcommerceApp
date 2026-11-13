import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authFetch } from "../utils/auth";
import { useCart } from "../context/CartContext";

function CheckoutPage() {
  // Fallback to 127.0.0.1:8000 if VITE_BASE_URL is missing, and remove any trailing slash
  const rawBaseUrl = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:8000";
  const BASEURL = rawBaseUrl.replace(/\/$/, "");

  const navigate = useNavigate();
  const cartContext = useCart() || {};
  const { clearCart } = cartContext;

  const [form, setForm] = useState({
    name: "",
    address: "",
    phone: "",
    payment_method: "COD",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [isError, setIsError] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setIsError(false);

    try {
      const res = await authFetch(`${BASEURL}/api/orders/create/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      // Safely parse response in case server returns HTML instead of JSON
      const text = await res.text();
      let data = {};
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(`Server returned status ${res.status} (Check API URL in urls.py)`);
      }

      if (res.ok) {
        setIsError(false);
        alert("Order placed successfully!");
        setMessage(`Order placed successfully! (Order #${data.order_number || data.order_id})`);

        if (typeof clearCart === "function") {
          clearCart();
        }

        navigate("/");
      } else {
        setIsError(true);
        setMessage(data.error || data.detail || "Failed to place order. Please try again.");
      }
      
    } catch (error) {
      console.error("Checkout error:", error);
      setIsError(true);
      setMessage(error.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-6">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">Checkout</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={form.name}
            onChange={handleChange}
            required
            className="w-full border rounded-lg p-2"
          />

          <textarea
            name="address"
            placeholder="Full Address"
            value={form.address}
            onChange={handleChange}
            required
            className="w-full border rounded-lg p-2"
          />

          <input
            type="tel"
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
            required
            className="w-full border rounded-lg p-2"
          />

          <select
            name="payment_method"
            value={form.payment_method}
            onChange={handleChange}
            className="w-full border rounded-lg p-2"
          >
            <option value="COD">Cash on Delivery</option>
            <option value="card">Online Payment</option>
          </select>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-300"
          >
            {loading ? "Processing..." : "Place Order"}
          </button>

          {message && (
            <p
              className={`text-center font-semibold mt-4 ${
                isError ? "text-red-600" : "text-green-700"
              }`}
            >
              {message}
            </p>
          )}
        </form>
      </div>
    </div>
  );
}

export default CheckoutPage;