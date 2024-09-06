/**
 * v0 by Vercel.
 * @see https://v0.dev/t/GCgfPNHTfoM
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet"

export default function Component() {
  return (
    <header className="flex h-16 w-full items-center justify-between bg-background px-4 shadow-md sm:px-6 md:px-8">
      <Link href="#" className="flex items-center gap-2" prefetch={false}>
        <span className="text-lg font-semibold">SOLARWISE</span>
      </Link>
      <nav className="hidden items-center gap-6 md:flex">
        <Link
          href="#"
          className="text-sm font-medium transition-colors hover:text-primary"
          prefetch={false}
        >
          Home
        </Link>
        <Link
          href="#"
          className="text-sm font-medium transition-colors hover:text-primary"
          prefetch={false}
        >
          Products
        </Link>
        <Link
          href="#"
          className="text-sm font-medium transition-colors hover:text-primary"
          prefetch={false}
        >
          About
        </Link>
        <Link
          href="#"
          className="text-sm font-medium transition-colors hover:text-primary"
          prefetch={false}
        >
          Contact
        </Link>
      </nav>
      <div className="hidden items-center gap-4 md:flex">
        <Button variant="outline" size="sm" className="hidden md:inline-flex">
          Sign Up
        </Button>
        <Button variant="ghost" size="icon" className="md:hidden">
          <MenuIcon className="h-6 w-6" />
          <span className="sr-only">Toggle menu</span>
        </Button>
        <Button variant="ghost" size="icon">
          <MoonIcon className="h-6 w-6" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </div>
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="md:hidden">
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="right" className="w-[300px]">
          <div className="flex h-16 items-center justify-between px-4">
            <Link href="#" className="flex items-center gap-2" prefetch={false}>
              <span className="text-lg font-semibold">SolarWise</span>
            </Link>
            <Button variant="ghost" size="icon">
              <MoonIcon className="h-6 w-6" />
              <span className="sr-only">Toggle theme</span>
            </Button>
          </div>
          <nav className="grid gap-4 px-4 py-6">
            <Link
              href="#"
              className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
              prefetch={false}
            >
              Home
            </Link>
            <Link
              href="#"
              className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
              prefetch={false}
            >
              Products
            </Link>
            <Link
              href="#"
              className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
              prefetch={false}
            >
              About
            </Link>
            <Link
              href="#"
              className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
              prefetch={false}
            >
              Contact
            </Link>
          </nav>
          <div className="border-t px-4 py-4">
            <Button variant="outline" size="sm" className="w-full">
              Sign Up
            </Button>
          </div>
        </SheetContent>
      </Sheet>
    </header>
  )
}

function MenuIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  )
}

function MoonIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
    </svg>
  )
}
