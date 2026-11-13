import { Link } from "react-router-dom";

function ProductCard({ product }) {
  const name = product?.title ?? product?.name ?? product?.product_name ?? "Unnamed Product";
  const price = product?.sale_price ?? product?.price ?? product?.unit_price ?? 0;
  const image = product?.image_url ?? product?.image ?? "";

  const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL || "http://127.0.0.1:8000";

  const imageUrl = (() => {
    if (!image) return "";
    if (image.startsWith("http://") || image.startsWith("https://")) return image;
    return `${BASEURL}${image.startsWith("/") ? "" : "/"}${image}`;
  })();

  return (
    <Link to={`/product/${product.id}`}>
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg hover:scale-[1.02] transition-transform p-4 cursor-pointer">
      <div className="mb-4 h-56 overflow-hidden rounded-lg bg-gray-100">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-full object-cover"
          />
        ) : null}
    </div>

      <h2 className="text-lg font-semibold text-gray-800 truncate">{name}</h2>
      <p className="text-gray-600 font-medium">${Number(price).toFixed(2)}</p>
    </div>
    </Link>
  );
}

export default ProductCard;