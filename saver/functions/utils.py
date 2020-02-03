import sys


def show_progress_download(stream, chunk, file_handle, bytes_remaining):
    """
    simple status of progress
    :param stream: An instance of :class:`Stream <Stream>` being downloaded, :py:class:`pytube.Stream`
    :param chunk: Segment of media file binary data, not yet written to disk.
    :param file_handle: The file handle where the media is being written to. :py:class:`io.BufferedWriter`
    :param bytes_remaining: How many bytes have been downloaded.
    """
    size = stream.filesize
    bytes_downloaded = size - bytes_remaining
    percentage_of_completion = bytes_downloaded / size * 100
    status = '#' * int((percentage_of_completion / 10))
    if percentage_of_completion != 100:
        sys.stdout.write('\r' + '    ↳[{status}] {percent}% Downloading...'.format(status=status, percent=int(percentage_of_completion)))
        sys.stdout.flush()
    else:
        sys.stdout.write('\r' + '    ↳[{status}] {percent}% Complete...\n'.format(status=status, percent=int(percentage_of_completion)))
        sys.stdout.flush()
