from math import ceil


def justified_line_stream(line, maxlen, spaces=None, last_line=False):
    if not last_line:
        # Quiz: How do you split m things amongst n people in a line
        # such that all but the last person get at least one thing, but
        # those further left get the most, progressively? (Below is a
        # hint.)
        space_groups = len(line) - 1  # Regions to split spaces.
        for word in line:
            if spaces and space_groups:
                word_space = ceil(spaces / space_groups)
                yield word + (" " * word_space)
                spaces -= word_space
                space_groups -= 1
            else:
                yield word + "\n"
    # Don't justify the last line, and don't add a newline.
    else:
        yield " ".join(line)
                

    
def justified_text_stream(words, maxlen):
    # Account for appended newline after each line.
    # Each line's len <= maxlen + 1, "1" due to each line but the last
    # having a newline.
    line_len = maxlen + 1
    line = []
    words_len = 0
    words_seen = 0
    for word in words:
        if (remainder := (line_len - len(word) - 1)) > 0:
            line.append(word)
            line_len = remainder
            words_len += len(word)
        else:
            yield from justified_line_stream(
                line, maxlen, spaces=maxlen - words_len
            )
            # Start building a new line.
            # NOTE: Handle breaking up word if word > maxlen.
            line = [word]
            # Set to current word length.
            words_len = len(word)
            line_len = maxlen + 1 - len(word)
            
        words_seen += 1
        if words_seen == len(words):
            # You're at the last line.
            yield from justified_line_stream(
                line, maxlen, last_line=True
            )
    

def justify_text(text, maxlen=30, return_list=False):
    words = text.split(" ")
    if maxlen < len(words[0]):
        # Re-use the default.
        maxlen = 30   
    justified_text = justified_text_stream(words,maxlen)
    if return_list:
        return list(justified_text)
    return "".join(justified_text)
