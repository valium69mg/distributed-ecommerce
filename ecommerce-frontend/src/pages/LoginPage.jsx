import LoginForm from "../components/LoginForm";
import "../App.css";

export default function LoginPage() {
  return (
    <div className="page">
      <header></header>
      <main className="content">
        <LoginForm />
      </main>
      <footer></footer>
    </div>
  );
}
