import Link from "next/link";
import Image from "next/image";
import cargo from "@/public/cargo.avif";

export default function Page() {
  return (
    <main className="mt-30  w-full h-[90vh]">
      <Image
        src={cargo}
        fill
        placeholder="blur"
        quality={100}
        className="object-cover object-top"
        alt="Mountains and forests with two cabins"
       
      />

<div className="relative z-10 text-center">
  <h1 className="text-8xl text-amber-100 mb-20 tracking-tight font-normal">
    Welcome to Cargo Site
  </h1>

  <Link
    href="/dashboard"
    className=" bg-accent-500 border-2 border-primary-900 px-8 py-6
               text-amber-100 text-lg font-semibold rounded-xl
               shadow-md hover:shadow-lg hover:bg-accent-600 transition-all"
  >
          Manage your Business
        </Link>
      </div>
    </main>
  );
}
