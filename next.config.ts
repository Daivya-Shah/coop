import type { NextConfig } from "next";

// Static export: `npm run build` writes a plain site to out/ that any host can serve.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
};

export default nextConfig;
