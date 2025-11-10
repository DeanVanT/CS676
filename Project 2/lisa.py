import openai
import os
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.environment import TinyWorld
from tinytroupe.examples import create_lisa_the_data_scientist

class LisaTheDataScientist:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in your environment variables.")
        
        self.client = openai.OpenAI(api_key=api_key)  # Initialize OpenAI client
        self.system_prompt = (
            "You are Lisa, a data scientist who is helpful, knowledgeable, and slightly sarcastic. "
            "You specialize in Python, pandas, and SQL."
        )
        self.chat_history = [{"role": "system", "content": self.system_prompt}]
    
    def listen_and_act(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.chat_history
        )
        reply = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": reply})
        return reply

if __name__ == "__main__":

    '''
    # Original Lisa conversation code - DO NOT MODIFY
    lisa = LisaTheDataScientist()
    print("Chat with Lisa (type 'quit' or 'exit' to end the conversation)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("Lisa: Goodbye! May your data always be clean and your queries always be fast.")
            break
        
        if not user_input:
            continue
        
        response = lisa.listen_and_act(user_input)
        print(f"Lisa: {response}\n")
    '''

    # Use pre-packaged Lisa persona
    lisa = create_lisa_the_data_scientist()
    
    # Create Danilo using factory
    factory = TinyPersonFactory("A hospital in São Paulo, Brazil.")
    danilo = factory.generate_person("Create a Brazilian man named Danilo that is a radiologist, likes pets and nature and loves heavy metal.")
    
    print("=" * 80)
    print("CONVERSATION BETWEEN LISA AND DANILO")
    print("=" * 80)
    
    # Simple back-and-forth conversation
    print("\n[Lisa introduces herself to Danilo]")
    lisa_intro = lisa.listen_and_act("Introduce yourself to Danilo, a radiologist you just met.")
    print(f"Lisa: {lisa_intro}")
    
    print("\n[Danilo responds]")
    danilo_response = danilo.listen_and_act(f"Lisa just said: '{lisa_intro}'. Respond to her introduction and tell her about yourself.")
    print(f"Danilo: {danilo_response}")
    
    print("\n[Lisa asks about his interests]")
    lisa_question = lisa.listen_and_act(f"Danilo said: '{danilo_response}'. Ask him about his hobbies and interests.")
    print(f"Lisa: {lisa_question}")
    
    print("\n[Danilo talks about heavy metal and pets]")
    danilo_hobbies = danilo.listen_and_act(f"Lisa asked: '{lisa_question}'. Tell her about your love for heavy metal music and your pets.")
    print(f"Danilo: {danilo_hobbies}")
    
    print("\n" + "=" * 80)