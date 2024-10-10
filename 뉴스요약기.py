import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from openai import OpenAI
import platform

class NewsSummarizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("News 요약기")
        
        # API Key input
        self.api_key_label = tk.Label(master, text="OpenAI API Key:")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(master, width=50, show="*")
        self.api_key_entry.pack()
        
        # URL input
        self.url_label = tk.Label(master, text="뉴스 기사 URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()
        
        # Summarize button
        self.summarize_button = tk.Button(master, text="Summarize", command=self.summarize_article)
        self.summarize_button.pack()
        
        # Output area
        self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.output_area.pack()

    def summarize_article(self):
        api_key = self.api_key_entry.get()
        url = self.url_entry.get()
        
        if not api_key or not url:
            messagebox.showerror("Error", "Please enter both API key and URL")
            return
        
        try:
            # Fetch article content
            response = requests.get(url)
            article_content = response.text
            
            # Use OpenAI API to summarize
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "너는 뉴스 기사를 요약하고 인사이트를 제공하는 유용한 어시스턴트야."},
                    {"role": "user", "content": f"해당 뉴스 기사를 요약하고 인사이트를 제공해줘. 내가 제공하는 기사 자료를 참고해서 요점, 주요 사실, 중요한 시사점 또는 트렌드에 초점을 맞춰야해. 기사 자료: {article_content}"}
                ],
                max_tokens=5000
            )
            
            summary = response.choices[0].message.content
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, summary)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = NewsSummarizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    if platform.system() == "Darwin":  # macOS
        import os
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
    main()
