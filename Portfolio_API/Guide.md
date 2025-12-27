# source code này sẽ copy qua folder AI-Portfolio-API để deploy lên huggingface
- và code sẽ push lên repo trên huggingface
- trên thư mục hiện tại thì push lên github repo để quản lý riêng

# sau khi deploy lên huggingface thì api sẽ là:
- https://<account>-<repo name>.hf.space/
- https://nult2003-ai-portfolio-api.hf.space/
- api connect với supabase cloud qua pooler session

# run  docker file
- docker run -d --name portfolio-api -p 7860:7860 portfolio-api

