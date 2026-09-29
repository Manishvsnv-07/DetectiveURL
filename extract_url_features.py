from urllib.parse import urlparse, urlunparse
import re


def normalize_url(url):
    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    if (
        parsed.path == "/"
        and not parsed.query
        and not parsed.fragment
    ):
        parsed = parsed._replace(path="")

    return urlunparse(parsed)

def extract_url_features(url):


    url = normalize_url(url)

    if not url.startswith(("http://", "https://")):
        url_for_parse = "http://" + url
    else:
        url_for_parse = url

    parsed = urlparse(url_for_parse)

    domain = parsed.netloc
    domain_without_port = domain.split(":")[0]

    url_length = len(url)

    domain_length = len(domain_without_port)

    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    is_domain_ip = int(
        bool(re.match(ip_pattern, domain_without_port))
    )

    domain_parts = [
        part
        for part in domain_without_port.split(".")
        if part
    ]

    if len(domain_parts) >= 3:
        no_of_subdomain = len(domain_parts) - 2
    else:
        no_of_subdomain = 0

    no_of_letters = sum(
        c.isalpha()
        for c in url
    )

    no_of_digits = sum(
        c.isdigit()
        for c in url
    )

    digit_ratio = (
        no_of_digits / url_length
        if url_length > 0
        else 0
    )

    no_of_dots = url.count(".")

    no_of_hyphens = url.count("-")

    no_of_slashes = url.count("/")

    no_of_equals = url.count("=")

    no_of_qmark = url.count("?")

    no_of_ampersand = url.count("&")

    no_of_special_chars = sum(
        not c.isalnum()
        for c in url
    )

    has_at_symbol = int(
        "@" in url
    )

    is_https = int(
        url.lower().startswith("https://")
    )

    try:
        has_port = int(
            parsed.port is not None
        )
    except ValueError:
        has_port = 1


    path = parsed.path

    path_length = len(path)

    path_segments = [
        segment
        for segment in path.split("/")
        if segment
    ]

    no_of_path_segments = len(
        path_segments
    )

    digit_sequences = re.findall(
        r"\d+",
        url
    )

    if digit_sequences:

        max_digit_sequence_length = max(
            len(sequence)
            for sequence in digit_sequences
        )

    else:

        max_digit_sequence_length = 0

    has_long_numeric_token = int(
        max_digit_sequence_length >= 5
    )

    suspicious_words = [
        "login",
        "signin",
        "verify",
        "verification",
        "account",
        "update",
        "secure",
        "bank",
        "password",
        "confirm",
        "free",
        "bonus",
        "winner",
        "claim",
        "support"
    ]

    suspicious_text = (
        parsed.path
        + "?"
        + parsed.query
    ).lower()

    suspicious_word_count = sum(
        suspicious_text.count(word)
        for word in suspicious_words
    )

    return {

        "URLLength": url_length,

        "DomainLength": domain_length,

        "IsDomainIP": is_domain_ip,

        "NoOfSubDomain": no_of_subdomain,

        "NoOfLettersInURL": no_of_letters,

        "NoOfDegitsInURL": no_of_digits,

        "DigitRatioInURL": digit_ratio,

        "NoOfDots": no_of_dots,

        "NoOfHyphens": no_of_hyphens,

        "NoOfSlashes": no_of_slashes,

        "NoOfEquals": no_of_equals,

        "NoOfQMark": no_of_qmark,

        "NoOfAmpersand": no_of_ampersand,

        "NoOfSpecialChars": no_of_special_chars,

        "HasAtSymbol": has_at_symbol,

        "IsHTTPS": is_https,

        "HasPort": has_port,

        "PathLength": path_length,

        "NoOfPathSegments": no_of_path_segments,

        "MaxDigitSequenceLength": max_digit_sequence_length,

        "HasLongNumericToken": has_long_numeric_token,

        "SuspiciousWordCount": suspicious_word_count
    }