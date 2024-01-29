import axios from "axios";
import { Button } from "@/components/ui/button";
import { useState, useEffect, ChangeEvent } from "react";
import { TransactionsTable } from "@/components/Table";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface FormData {
  user_did: string;
  phone_number: string;
  plan: string;
  provider: string;
  usage: number;
}
interface JsonData {
  user_did: string;
  hashed_phone_number: string;
  plan: string;
  provider: string;
  signature: string;
}

export function Login({ provider }: { provider: string }) {
  const [transactions, setTransaction] = useState<any[]>([]);
  const [formData, setFormData] = useState<FormData>({
    user_did: "enter your name",
    phone_number: "09xxxxxxxx",
    plan: "which Plan",
    provider: provider,
    usage: 0,
  });
  const [JsonData, setJsonData] = useState<JsonData>({
    user_did: "did:example:789abcdefghi",
    hashed_phone_number: "hufaesuhoefhuiw",
    plan: "Bac",
    provider: "elecom",
    signature: "wq",
  });

  useEffect(() => {
    console.log(JsonData);
    console.log(formData);
  }, [JsonData, formData]);

  const isSignUpNAN =
    formData.phone_number === "" ||
    formData.user_did === "" ||
    formData.plan === "" ||
    formData.provider === "";

  const isLoginNAN = formData.phone_number === "" || formData.user_did === "";
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.id === "usage") {
      setFormData({
        ...formData,
        [e.target.id]: parseInt(e.target.value),
      });
    } else {
      setFormData({
        ...formData,
        [e.target.id]: e.target.value,
      });
    }
  };
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        try {
          const text = e.target?.result;
          const jsonData = text ? JSON.parse(text.toString()) : null;
          if (jsonData) {
            console.log(jsonData);
            // Process your JSON data here
            // For example, updating the formData state
            setJsonData(jsonData as JsonData);
          }
        } catch (err) {
          console.error("Error parsing JSON:", err);
        }
      };
      reader.readAsText(file);
    }
  };
  const HandleDID = async () => {
    console.log("click");
    try {
      if (
        JsonData.provider === "A_Telecom" ||
        JsonData.provider === "B_Telecom" ||
        JsonData.provider === "C_Telecom"
      ) {
        if (JsonData.provider === provider) {
          alert("You are already the member of this telecom");
          return;
        }
        //link to vietel
        alert("Login success");
        await axios.post(`http://127.0.0.1:5000/${provider}/transaction/add`, {
          user_did: JsonData.user_did,
          provider: JsonData.provider,
          signature: JsonData.signature,
          plan: JsonData.plan,
          phone_number: JsonData.hashed_phone_number,
          usage: formData.usage,
        });
      } else {
        alert("Wrong user name or phone number");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const SignUpDID = async () => {
    console.log("click");
    try {
      const res = await axios.post("http://127.0.0.1:5000/add_user", formData);
      console.log(res.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  useEffect(() => {
    const GetTransaction = async () => {
      console.log("click");
      try {
        const transaction = await axios.get(
          `http://127.0.0.1:5000/${provider}/transaction/get`
        );
        setTransaction(transaction.data.TRANSACTIONS);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    GetTransaction();
  }, [provider]);
  return (
    <div>
      <Tabs defaultValue="Login" className="w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="Sign up">Sign up</TabsTrigger>
          <TabsTrigger value="Login">Verify</TabsTrigger>
        </TabsList>
        <TabsContent value="Sign up">
          <Card>
            <CardHeader>
              <CardTitle>Sign up</CardTitle>
              <CardDescription>
                Make sure ypur have already registered with your Telcom
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="user_did">Name</Label>
                <Input
                  id="user_did"
                  defaultValue={formData.user_did}
                  onChange={(e) => handleChange(e)}
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input
                  id="phone_number"
                  defaultValue={formData.phone_number}
                  onChange={(e) => handleChange(e)}
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="plan">Plan</Label>
                <Input
                  id="plan"
                  defaultValue={formData.plan}
                  onChange={(e) => handleChange(e)}
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button onClick={SignUpDID} disabled={isSignUpNAN}>
                Sign up
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="Login">
          <Card>
            <CardHeader>
              <CardTitle>Get Service</CardTitle>
              <CardDescription>Get DID from your Telcom</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="fileUpload">Upload JSON File</Label>
                <Input
                  id="fileUpload"
                  type="file"
                  accept=".json"
                  onChange={(e) => handleFileChange(e)}
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="usage">usage</Label>
                <Input
                  id="usage"
                  type="number"
                  defaultValue={formData.usage}
                  onChange={(e) => handleChange(e)}
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button onClick={HandleDID} disabled={isLoginNAN}>
                Get Service
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
      <TransactionsTable transactions={transactions} />
    </div>
  );
}
