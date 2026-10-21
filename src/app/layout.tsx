import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import { JoinProvider } from "@/components/Join";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], axes: ["opsz"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Coop — Because every flock needs one",
  description:
    "Coop brings NYC clubs and neighborhood spots together. Clubs find somewhere to keep coming back to; restaurants, bars and cafés get a few more familiar faces.",
};

export const viewport: Viewport = { themeColor: "#ffffff" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <JoinProvider>{children}</JoinProvider>
      </body>
    </html>
  );
}
