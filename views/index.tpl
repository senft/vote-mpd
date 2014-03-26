<!DOCTYPE html>
<html>
<head>
    <title>YEAH</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link rel="stylesheet" type="text/css" href="static/main.css" />
    <link rel="stylesheet" type="text/css" media="screen and (max-width: 480px)" href="static/mobile.css">

    <script src="static/jquery-2.0.2.min.js"></script>
    <!--<script src="static/bootstrap/js/bootstrap.min.js"></script>-->
    <script type="text/javascript" src="/static/jquery-ui-1.10.3.custom.js"></script>
    <script type="text/javascript" src="/static/jquery.dataTables.min.js"></script> 

<script type="text/javascript">
</script>

    <script type="text/javascript">
        //var timedRefresh = setTimeout(function(){location.reload(true)},{{remaining_time}});

      $(document).ready(function() 
        { 
          $("tr.song-{{voted}} td").effect('highlight', {color: '#F0B49E'}, 1800);


          $("#playlist").dataTable({
            "sDom": '<"top"i>rt<"bottom"lp><"clear">',
            "bPaginate": false,
            "bInfo": false}
          ); 

          $("#playlist_filter").bind("keyup", function(event) {
            $("#playlist").dataTable().fnFilter($(this).val().trim());
          });

        } 
      );

    </script>

</head>

<body>

  <div id="main">

    <div class="row">
      <div class="sidebar">
        Currently playing:
      </div>
      <div id="current">
          {{current_song['artist']}} - {{current_song['title']}}
      </div>
    </div>

    <div class="row">
      <div class="sidebar">
        Queue:
      </div>
      <form action="/" method="post" enctype="multipart/form-data">
      <table id="next" cellspacing="0">
        <tr class="current">
          <td class="info"><img src="static/playing.gif" />
          <td class="artist">{{current_song['artist']}}</td>
          <td class="title">{{current_song['title']}}</td>
        </tr>

      %for i, song in enumerate(next_songs):
        %if i % 2 == 0:
          <tr class="odd voteable song-{{song['id']}}">
        %else:
          <tr class="even voteable song-{{song['id']}}">
        %end

          <td class="info">
            <button type="submit" value="{{song['id']}}" name="vote">{{song['pos']}}.</button>
          </td>
          <td class="artist">
            <button type="submit" value="{{song['id']}}" name="vote">{{song['artist']}}</button>
          </td>


          <td class="title">
            <button type="submit" value="{{song['id']}}" name="vote">{{song['title']}}</button>
          </td>
        </tr>
      %end
      </table>
      </form>
    </div>

    <div class="row smallgap">
      <div class="sidebar">&nbsp;</div>
      <div id="search">
        <form class="navbar-search pull-right">
          <input type="text" id="playlist_filter" class="search-query" placeholder="Search">
        </form>
      </div>
    </div>

    <div class="row">

      <div class="sidebar">
        Playlist:
      </div>
      <form action="/" method="post" enctype="multipart/form-data">
      <table id="playlist" cellspacing="0">
        <thead>
          <tr>
            <th>Artist</th>
            <th>Title</th>
          </tr>
        </thead>
        <tbody class="">
      %for i, song in enumerate(songs):
        %if i % 2 == 0:
        <tr class="voteable song-{{song['id']}}">
        %else:
        <tr class="voteable song-{{song['id']}}">
        %end
          <td class="artist">
            <button type="submit" value="{{song['id']}}" name="vote">{{song['artist']}}</button>
          </td>

          <td class="title">
            <button type="submit" value="{{song['id']}}" name="vote">{{song['title']}}</button>
          </td>
        </tr>
      %end
        </tbody>
      </table>
      </form>
   </div>

  </div>

</body>
