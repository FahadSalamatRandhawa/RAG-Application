"use client"
import { Input } from "@/components/ui/input";
import Image from "next/image";
import Link from "next/link";
import { useRef, useState } from "react";

export default function Home() {
  const [files,setFiles]=useState<FileList|null>(null)
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
      <Input
        type="file" multiple
      onChange={(e)=>setFiles(e.target.files)} />
      <button disabled={!files} onClick={handle_File_Upload} >Button</button>
    </main>
  );
}
