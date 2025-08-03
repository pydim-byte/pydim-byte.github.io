<%*
  let title = tp.file.title
  if (title.startsWith("Untitled")) {
    title = await tp.system.prompt("Title");
    await tp.file.rename(title);
  } 
  tR += "---"
%>
title: <%* tR += title %>
date: <% tp.date.now("yyyy-MM-DD") %> 
feed: <%* "show" %>
---