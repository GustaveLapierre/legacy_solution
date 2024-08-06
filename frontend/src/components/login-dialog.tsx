import { Form } from "react-router-dom";
import { useState } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";

export default function LoginDialog() {
  const [loginForm, setLoginForm] = useState({
    username: "",
    password: "",
  });

  const handleLogin = async () => {
    const form = new FormData();
    form.append("username", loginForm.username);
    form.append("password", loginForm.password);

    const response = await fetch("/api/login", {
      method: "POST",
      body: form,
    });
    if (!response.ok) {
      toast.error("Login failed");
    }
    toast.success("Login successful, redirecting...");
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  };

  return (
    <Dialog open>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="text-2xl text-center">Login</DialogTitle>
          <DialogDescription>Please login to continue</DialogDescription>
        </DialogHeader>
        <div>
          <Form onSubmit={handleLogin}>
            <div className="grid grid-rows-2 space-y-2">
              <div>
                <Label>Username</Label>
                <Input
                  type="email"
                  placeholder="Email address"
                  required
                  onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                />
              </div>
              <div>
                <Label>Password</Label>
                <Input
                  type="password"
                  placeholder="Password"
                  required
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                />
              </div>
            </div>
            <div className="my-4 text-center">
              <Button className="w-32">Login</Button>
            </div>
          </Form>
        </div>
      </DialogContent>
    </Dialog>
  );
}
