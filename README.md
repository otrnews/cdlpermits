# cdlpermits.com

Free CDL permit practice tests. Static site on GitHub Pages.

- Questions: questions.json (English) and questions_es.json (Spanish). Each question has q, a (right answer), w (wrong answers), e (explanation).
- Ads, links and state list: top of build.py.
- MyCDLCoach links on the results screen: top of quiz.js.

## Daily rebuild (question of the day, social image, RSS for Zapier)
Create the file `.github/workflows/build.yml` (Add file > Create new file, type that full name)
and paste in the contents of build.yml.txt. It rebuilds every morning and whenever questions change.

Zapier: use "RSS by Zapier" with https://cdlpermits.com/feed.xml, then post to Facebook and Instagram.
The daily image is https://cdlpermits.com/qotd-YYYY-MM-DD.png (in the feed item's enclosure).
