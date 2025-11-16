import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"
import { useLogin } from "../hooks/useLogin"
import "../index.css"

export default function LoginForm() {
  const loginMutation = useLogin()
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleSubmit = (e) => {
    e.preventDefault()
    const email = e.target.email.value
    const password = e.target.password.value

    loginMutation.mutate(
      { email, password },
      {
        onSuccess: (data) => {
          login(data.token) 
          navigate("/home")
        },
      }
    )
  }

  return (
    <Card className="w-[350px] h-[400px] mx-auto mt-20">
      <CardHeader>
        <h2 className="text-xl font-bold">Login</h2>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <Label htmlFor="email">Email</Label>
            <Input id="email" name="email" type="email" placeholder="you@example.com" />
          </div>
          <div className="mb-4">
            <Label htmlFor="password">Password</Label>
            <Input id="password" name="password" type="password" placeholder="••••••••" />
          </div>
          <Button type="submit" className="w-full" disabled={loginMutation.isLoading}>
            {loginMutation.isLoading ? "Signing In..." : "Sign In"}
          </Button>
          {loginMutation.isError && (
            <p className="text-red-500 text-sm mt-2">Login failed. Try again.</p>
          )}
        </form>
      </CardContent>
      <CardFooter>
        <p className="text-sm text-muted-foreground">
          Don’t have an account? <a href="/register" className="underline">Sign up</a>
        </p>
      </CardFooter>
    </Card>
  )
}
