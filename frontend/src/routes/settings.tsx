import { Form, useLoaderData } from "react-router-dom";
import { useState } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

type LoaderData = {
  id: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  username: string;
  created_at: string;
};

export default function Settings() {
  const data = useLoaderData() as LoaderData;
  const [formData, setFormData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  const handlePasswordChange = async () => {
    if (formData.newPassword.length < 8 && formData.confirmPassword.length < 8) {
      toast.error("Password must be at least 8 characters long");
      return;
    }
    const form = new FormData();
    form.append("currentPassword", formData.currentPassword);
    form.append("newPassword", formData.newPassword);
    form.append("confirmPassword", formData.confirmPassword);
    const res = await fetch("/api/change-password", {
      method: "POST",
      body: form,
    });

    if (!res.ok) {
      const result = await res.json();
      toast.error(result.message);
      return;
    }
    const result = await res.json();
    toast.success(result.message);

    setTimeout(async () => {
      const res = await fetch("/api/logout");
      if (res.ok) {
        window.location.href = "/";
      }
    }, 3000)
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-4 text-violet-900">Settings</h1>
      <h2 className="text-xl font-semibold  mt-4 text-violet-900">Basic Profile</h2>
      <table className="w-full">
        <tbody className="">
          <tr>
            <th className="text-start px-4 py-2">Name</th>
            <td>
              {data.first_name} {data.last_name}
            </td>
          </tr>
          <tr className="">
            <th className="text-start px-4 py-2">Username</th>
            <td>{data.username}</td>
          </tr>
          <tr>
            <th className="text-start px-4 py-2">Joined</th>
            <td>{new Date(data.created_at).toLocaleDateString()}</td>
          </tr>
          <tr>
            <th className="text-start px-4 py-2">Active</th>
            <td>{data.is_active ? "Yes" : "No"}</td>
          </tr>
        </tbody>
      </table>

      <h2 className="text-xl font-semibold  mt-8 text-violet-900">Change Password</h2>
      <section className="mt-2 mb-8">
        <Form className="space-y-4">
          <div>
            <Label>Current Password</Label>
            <Input
              placeholder="current password"
              type="password"
              required
              onChange={(e) => setFormData({ ...formData, currentPassword: e.target.value })}
            />
          </div>
          <div>
            <Label>New Password</Label>
            <Input
              placeholder="new password"
              type="password"
              required
              minLength={8}
              onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
            />
          </div>
          <div>
            <Label>Confirm Password</Label>
            <Input
              placeholder="confirm new password"
              type="password"
              required
              minLength={8}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
            />
          </div>
          <div className="flex justify-end">
            <Button onClick={handlePasswordChange}>Change Password</Button>
          </div>
        </Form>
      </section>
    </div>
  );
}
