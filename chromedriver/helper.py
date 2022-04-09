s = "<bound method PageElement.get_text of <h1>Готовый перевод One Piece: Like father like son! / Ван Пис: Каков отец, таков и сын: Глава 23 Многое произошло</h1>>"
title = s.replace("</h1>", "").replace(">", "").split("<h1>")[0].split("/")[-1].strip()
print(title)