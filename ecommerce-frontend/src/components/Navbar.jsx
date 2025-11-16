import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ShoppingCart } from "lucide-react"
import { DiReact } from "react-icons/di";
import { CiSearch } from "react-icons/ci";
import { useLogout } from "../hooks/useLogout"
import { useNavigate } from "react-router-dom"

export default function Navbar() {

  const logoutMutation = useLogout();
  const navigate = useNavigate()

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSuccess: () => {
        navigate("/login");
      },
    });
  };


  return (
    <header className="w-full border-b bg-white">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <DiReact size={24}/>
          <span className="font-bold text-xl">ShopMate</span>
        </div>

        {/* Search Bar */}
        <div className="flex flex-1 items-center px-4 space-x-2">
            <Input
                type="text"
                placeholder="Search products..."
                className="w-full"
            />
            <a className="cursor-pointer"> <CiSearch size={24}/> </a>    
        </div>


        {/* Categories Dropdown */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">Categories</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>Electronics</DropdownMenuItem>
            <DropdownMenuItem>Fashion</DropdownMenuItem>
            <DropdownMenuItem>Home & Kitchen</DropdownMenuItem>
            <DropdownMenuItem>Sports</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* User Section */}
        <div className="flex items-center space-x-4">
          {/* Cart */}
          <Button variant="ghost" size="icon">
            <ShoppingCart className="h-5 w-5" />
          </Button>

          {/* User Avatar */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Avatar>
                <AvatarImage src="/user.jpg" alt="User" />
                <AvatarFallback>U</AvatarFallback>
              </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Orders</DropdownMenuItem>
              <DropdownMenuItem><a onClick={handleLogout}>Logout</a></DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
