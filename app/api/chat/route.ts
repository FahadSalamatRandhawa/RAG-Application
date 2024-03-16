import { StreamingTextResponse, LangChainStream, Message } from 'ai';
import { ChatOpenAI } from 'langchain/chat_models/openai';
import { AIMessage, HumanMessage } from 'langchain/schema';
import { NextResponse } from 'next/server';

//export const runtime = 'edge';


export async function POST(req: Request) {
  const { messages } = await req.json();
  const currentMessageContent = messages[messages.length - 1].content;
  console.log(currentMessageContent)

  let vectorSearch=await fetch("http://localhost:3000/api/vectorsearch",{method:"POST",headers: {"Content-Type": "application/json"},body:JSON.stringify(currentMessageContent)})

  if(!vectorSearch.ok){
    return NextResponse.json({error:"Error in vector search"}, {status:500})
  }
  vectorSearch=await vectorSearch.json()

  const TEMPLATE=`
  You are an enthusiastic and helpful assistant who will answer the question according to the context The answer must be provided according to the context, otherwise respond with I don't know""" ,
  Question = ""${currentMessageContent}"",
  context = ""${vectorSearch}"" `

  messages[messages.length -1].content = TEMPLATE;

  const { stream, handlers } = LangChainStream();
  const llm = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    streaming: true,
  });
  
  llm
    .call(
      (messages as Message[]).map(m =>
        m.role == 'user'
          ? new HumanMessage(m.content)
          : new AIMessage(m.content),
      ),
      {},
      [handlers],
    )
    .catch(console.error);
  return new StreamingTextResponse(stream);
}