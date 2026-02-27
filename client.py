from groq import Groq

client = Groq(api_key="enter your groq api key here")

completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": "compose a poem that explains the concept of recursion in programming."}
    ]
)

print(completion.choices[0].message.content)