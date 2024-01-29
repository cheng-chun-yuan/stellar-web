"use client";
import { Login } from "@/components/Login";
import { useParams } from "next/navigation";
import React from "react";
const About: React.FC = () => {

  const telecom = useParams().telcomName?.toString();
  return (
    <div className="py-12 px-4">
      <div className="max-w-6xl mx-auto text-center">
        <h1 className="text-4xl font-semibold text-blue-600 mb-4">{telecom}</h1>
        <p className="text-lg text-gray-600 mb-8">Welcome to {telecom}</p>

          {/* Global Access for All */}
          <div className="flex justify-center">
            <h2 className="text-2xl font-semibold ml-2 mt-2">
              Global Access for All
            </h2>
          </div>
          <div className="flex justify-center mt-8">
            <Login provider={telecom} />
          </div>
        </div>
    </div>
  );
};

export default About;
