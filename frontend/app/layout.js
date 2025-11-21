import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {

  title:{
    template: "%s / Analytics Dashboard",
  default: "Welcome / Manage Successful Business",
},
description: 
"Order you favourite products at our reliable site.Make you day Perfect & Save you Time!",

};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className="bg-gray-50"
      >
       
        <div className="min-h-screen">

        {children}
        </div>
      </body>
    </html>
  );
}
