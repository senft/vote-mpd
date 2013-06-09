<html>
<head>
    <title>YEAH</title>

    <link rel="stylesheet" type="text/css" href="static/main.css" />
    <!-- <link rel="stylesheet" type="text/css" media="only screen and
(max-device-width: 480px)" href="static/mobile.css" /> -->
    <link rel="stylesheet" type="text/css" href="static/mobile.css" />

    <script type="text/javascript">
        //var timedRefresh = setTimeout(function(){location.reload(true)},1000)
    </script>

</head>

<body>

    <table class="playlist" border="0" cellpadding="0" cellspacing="0">
    %for song in songs:
      %if song['pos'] == '0':
        <tr class="current">
          <td class="vote" />
      %elif int(song['pos']) % 2 == 0:
        <tr class="even">
          <td class="vote"><a href="vote/{{song['id']}}">&uarr;</a></td>
      %else:
        <tr class="odd">
          <td class="vote"><a href="vote/{{song['id']}}">&uarr;</a></td>
      %end
        <td class="title"><a href="vote/{{song['id']}}">{{song['title']}}</a></td>
        <td class="divider">-</td>
        <td class="artist"><a href="vote/{{song['id']}}">{{song['artist']}}</a></td>
      </tr>
    %end
    </table>

</body>
