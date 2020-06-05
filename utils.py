import sys


def get_time_code(time_code):
    """
    Returns time codes
    :param time_code: ``str`` in the following format: ``mm:ss mm:ss`` or only start ``-mm:ss`` or only end ``mm:ss-``
    :return: ``Tuple([start_mm, start_ss], [end_mm, end_ss])``
    """
    time_code = time_code.split(' ')

    if len(time_code) == 2:
        start = time_code[0]
        end = time_code[-1]
    else:
        time_code = time_code[0]

        if time_code[0] == '-':
            start = time_code[1:]
            end = None

        elif time_code[-1] == '-':
            start = None
            end = time_code[:-1]

        else:
            start = None
            end = None
            return

    if start is None:
        start_mm = None
        start_ss = None
    else:
        start_mm = start.split(':')[0]
        start_ss = start.split(':')[-1]

    if end is None:
        end_mm = None
        end_ss = None
    else:
        end_mm = end.split(':')[0]
        end_ss = end.split(':')[-1]

    start = [start_mm, start_ss]
    end = [end_mm,  end_ss]
    return start, end


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
        sys.stdout.write('\r' + '    ↳[{status}] {percent}% Downloading...'.format(
            status=status, percent=int(percentage_of_completion)))
        sys.stdout.flush()
    else:
        sys.stdout.write('\r' + '    ↳[{status}] {percent}% Complete...\n'.format(
            status=status, percent=int(percentage_of_completion)))
        sys.stdout.flush()
