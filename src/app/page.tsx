"use client";
import { Login } from '@/components/Login'
import Link from 'next/link';
export default function Home() {
  return (
    <main className="flex flex-col items-center justify-between p-24">
      <p className="text-4xl font-bold mb-10">Welcome to Telecom Family</p>
      <div className="flex flex-row justify-center items-center space-x-4 mt-10">
        {/* Block 1 */}
        <div className="block p-10 text-2xl bg-gray-200 rounded">
          <Link href="/A_Telecom">
            A Telecom
          </Link>
        </div>

        {/* Block 2 */}
        <div className="block p-10 text-2xl bg-gray-200 rounded">
          <Link href="/B_Telecom">
            B Telecom
          </Link>
        </div>

        {/* Block 3 */}
        <div className="block p-10 text-2xl bg-gray-200 rounded">
          <Link href="/C_Telecom">
            C Telecom
          </Link>
        </div>
      </div>
    </main>
  )
}
