"use client"
import { Input } from "@/components/ui/input";
import Image from "next/image";
import Link from "next/link";
import { useRef, useState } from "react";
import { useChat } from "ai/react";
import { Button } from "@/components/ui/button";

export default function Home() {
  const [files,setFiles]=useState<FileList|null>(null)

  const { messages, input, handleInputChange, handleSubmit } = useChat();

  async function handle_File_Upload(){
    const formData = new FormData();
  
  // Append each file to the form data
  if(files)
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  console.log("Form data files",formData.getAll("files"))
    const response=await fetch('http://localhost:3000/api/upload',{method:"POST",body:formData})

    if(response.ok){
      console.log(response)
    }else{
      console.log("Error in uploading file")
    }
  }
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      
      {/* files upload section  */}
      <div className=" flex gap-5">
        <Input
          type="file" multiple
        onChange={(e)=>setFiles(e.target.files)} />
        <Button disabled={!files} onClick={handle_File_Upload} >Upload to db</Button>
      </div>

      {/* Chat section */}
      <div className="mx-auto w-full max-w-md py-24 flex flex-col stretch">
        {messages.length > 0
          ? messages.map((m) => (
              <div key={m.id} className="whitespace-pre-wrap">
                {m.role === "user" ? "User: " : "AI: "}
                <text>{m.content}</text>
              </div>
            ))
          : null}

        <form onSubmit={handleSubmit}>
          <input
            className="fixed w-full max-w-md bottom-0 border border-gray-300 rounded mb-8 shadow-xl p-2"
            value={input}
            placeholder="Say something..."
            onChange={handleInputChange}
          />
        </form>
      </div>
    </main>
  );
}
