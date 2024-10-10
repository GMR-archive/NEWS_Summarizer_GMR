import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
from openai import OpenAI
import platform

class NewsSummarizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("News 요약기")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for each tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.insights_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.summary_frame, text="요약")
        self.notebook.add(self.insights_frame, text="인사이트")
        
        self.setup_summary_tab()
        self.setup_insights_tab()
    
    def setup_summary_tab(self):
        # API Key input
        self.api_key_label = tk.Label(self.summary_frame, text="OpenAI API Key:")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(self.summary_frame, width=50, show="*")
        self.api_key_entry.pack()
        
        # URL input
        self.url_label = tk.Label(self.summary_frame, text="뉴스 기사 URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.summary_frame, width=50)
        self.url_entry.pack()
        
        # Summarize button
        self.summarize_button = tk.Button(self.summary_frame, text="Summarize", command=self.summarize_article)
        self.summarize_button.pack()
        
        # Output area
        self.summary_output = scrolledtext.ScrolledText(self.summary_frame, wrap=tk.WORD, width=60, height=15)
        self.summary_output.pack()
        
        # Additional input for refinement
        self.refinement_label = tk.Label(self.summary_frame, text="추가 의견:")
        self.refinement_label.pack()
        self.refinement_entry = tk.Entry(self.summary_frame, width=50)
        self.refinement_entry.pack()
        
        # Refine button
        self.refine_button = tk.Button(self.summary_frame, text="Refine Summary", command=self.refine_summary)
        self.refine_button.pack()
    
    def setup_insights_tab(self):
        self.insights_output = scrolledtext.ScrolledText(self.insights_frame, wrap=tk.WORD, width=60, height=20)
        self.insights_output.pack()

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
            
            # Use OpenAI API to summarize and provide insights
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "너는 뉴스 기사를 요약하고 인사이트를 제공하는 유용한 어시스턴트야. 요약과 인사이트를 명확히 구분해서 제공해야 해."},
                    {"role": "user", "content": f"""다음 뉴스 기사에 대해 요약과 인사이트를 제공해줘. 다음 형식을 따라줘:

요약:
[여기에 간결한 요약을 작성해줘. 주요 사실과 핵심 포인트만 포함시켜야해

인사이트:
[여기에 기사의 함의, 중요한 시사점, 관련 트렌드 등을 분석해줘.]

기사 내용: {article_content}"""}
                ],
                max_tokens=5000
            )
            
            result = response.choices[0].message.content
            
            # Split summary and insights
            summary_part = result.split("인사이트:")[0].replace("요약:", "").strip()
            insights_part = result.split("인사이트:")[1].strip() if "인사이트:" in result else ""
            
            self.summary_output.delete(1.0, tk.END)
            self.summary_output.insert(tk.END, summary_part)
            
            self.insights_output.delete(1.0, tk.END)
            self.insights_output.insert(tk.END, insights_part)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refine_summary(self):
        api_key = self.api_key_entry.get()
        refinement = self.refinement_entry.get()
        current_summary = self.summary_output.get(1.0, tk.END)
        
        if not api_key or not refinement:
            messagebox.showerror("Error", "Please enter API key and refinement request")
            return
        
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "너는 뉴스 기사 요약을 개선하는 유용한 어시스턴트야."},
                    {"role": "user", "content": f"다음 요약을 주어진 의견에 따라 수정해줘: \n\n요약: {current_summary}\n\n의견: {refinement}"}
                ],
                max_tokens=5000
            )
            
            refined_summary = response.choices[0].message.content
            
            self.summary_output.delete(1.0, tk.END)
            self.summary_output.insert(tk.END, refined_summary)
        
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
