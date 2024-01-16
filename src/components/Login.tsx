import axios from 'axios'
import { Button } from "@/components/ui/button"
import { useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"

export function Login() {
  const [formData, setFormData] = useState({
    userName: 'enter your name',
    phoneNumber: '09xxxxxxxx',
    plan: 'which Plan',
    provider: '--- Telecom',
  });

  const isSignUpNAN = formData.phoneNumber==="" || formData.userName==="" || formData.plan==="" || formData.provider==="";

  const isLoginNAN = formData.phoneNumber==="" || formData.userName==="" ;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
    console.log(formData);
  };
  const HandleDID = async () => {
    console.log('click');
    try {
      const res = await axios.get(`http://127.0.0.1:5000/get_provider/${formData.phoneNumber}/${formData.userName}`);
      console.log(res.data);
      if (res.data === 'Taiwan_Telecom') {
        //link to vietel
        window.location.href = './Taiwan_Telecom';
      } else if (res.data === 'taiwan101') {
        //link to vina
        window.location.href = './taiwan101';
      }
      else if (res.data === 'chunghau') {
        //link to mobi
        window.location.href = './chunghau';
      }
      else{
        alert('Wrong user name or phone number');
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const SignUpDID = async () => {
    console.log('click');
    try {
        const res = await axios.post('http://127.0.0.1:5000/add_user', formData);
        console.log(res.data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
  };
  return (
    <Tabs defaultValue="Sign up" className="w-[400px]">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="Sign up">Sign up</TabsTrigger>
        <TabsTrigger value="Login">Login</TabsTrigger>
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
              <Label htmlFor="userName">Name</Label>
              <Input id="userName" defaultValue={formData.userName}  onChange={(e)=>handleChange(e)}/>
            </div>
            <div className="space-y-1">
              <Label htmlFor="phoneNumber">PhoneNumber</Label>
              <Input id="phoneNumber" defaultValue={formData.phoneNumber} onChange={(e)=>handleChange(e)}/>
            </div>
            <div className="space-y-1">
              <Label htmlFor="plan">Plan</Label>
              <Input id="plan" defaultValue={formData.plan}  onChange={(e)=>handleChange(e)}/>
            </div>
            <div className="space-y-1">
              <Label htmlFor="provider">Provider</Label>
              <Input id="provider" defaultValue={formData.provider}  onChange={(e)=>handleChange(e)}/>
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={SignUpDID} disabled={isSignUpNAN}>Sign up</Button>
          </CardFooter>
        </Card>
      </TabsContent>
      <TabsContent value="Login">
        <Card>
          <CardHeader>
            <CardTitle>Login</CardTitle>
            <CardDescription>
                Get DID from your Telcom
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="space-y-1">
              <Label htmlFor="current">Username</Label>
              <Input id="userName" defaultValue={formData.userName} onChange={(e)=>handleChange(e)}/>
            </div>
            <div className="space-y-1">
              <Label htmlFor="new">PhoneNumber</Label>
              <Input id="phoneNumber"  defaultValue={formData.phoneNumber} onChange={(e)=>handleChange(e)}/>
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={HandleDID} disabled={isLoginNAN}>Login</Button>
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  )
}
