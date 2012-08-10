# pls-files

This script will list the audio files/streams in the given .pls playlist(s), in a format that can be piped directly to `mpc add`.

## Examples

    monogram:~ ahihi$ pls-files Foldplop\ -\ Totem\ EP/playlist.pls 
    file:///Users/ahihi/Foldplop - Totem EP/01 Connect.flac
    file:///Users/ahihi/Foldplop - Totem EP/02 Synchronise.flac
    file:///Users/ahihi/Foldplop - Totem EP/03 Blossom.flac
    file:///Users/ahihi/Foldplop - Totem EP/04 Unwind.flac

    monogram:~ ahihi$ pls-files http://radio.radiohelsinki.fi/listen2.pls
    http://radio1.radiohelsinki.fi/rh256

    monogram:~ ahihi$ pls-files Foldplop\ -\ Totem\ EP/playlist.pls http://radio.radiohelsinki.fi/listen2.pls | mpc add -v
    adding: file:///Users/ahihi/Foldplop - Totem EP/01 Connect.flac
    adding: file:///Users/ahihi/Foldplop - Totem EP/02 Synchronise.flac
    adding: file:///Users/ahihi/Foldplop - Totem EP/03 Blossom.flac
    adding: file:///Users/ahihi/Foldplop - Totem EP/04 Unwind.flac
    adding: http://radio1.radiohelsinki.fi/rh256
