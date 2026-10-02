# cdlpermits.com

Free CDL permit practice tests. Static site on GitHub Pages, same idea as OTR News.

## Go live
1. In your GitHub account, create a new public repo named `cdlpermits`.
2. Upload everything in this folder (including the hidden `.github` folder) to the repo.
3. Repo Settings > Pages: Source = "Deploy from a branch", Branch = `main`, folder `/ (root)`. Save.
4. Same page, Custom domain: `cdlpermits.com`. Save, then tick "Enforce HTTPS" once it's available.
5. At GoDaddy, DNS for cdlpermits.com:
   - Four A records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME record `www` pointing to `<your-github-username>.github.io`
6. Submit https://cdlpermits.com/sitemap.xml in Google Search Console.

## Add or fix questions
Edit `questions.json` on GitHub. Each question has `q` (question), `a` (correct answer),
`w` (wrong answers) and `e` (explanation). Answers are shuffled automatically.
When you save, the "Rebuild site" action regenerates every page.
