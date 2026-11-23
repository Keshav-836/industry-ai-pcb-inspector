from core.aligner import align_to_reference
from core.annotator import draw_results, to_data_url
from core.comparator import compare_parts


def inspect_image(reference, parts, test):
    # poora flow ek jagah: align -> compare -> boxes draw -> result
    aligned, align_info = align_to_reference(reference, test)
    comparison = compare_parts(reference, aligned, parts)
    annotated = draw_results(aligned, comparison)

    result = {
        "status": comparison["status"],
        "missing_parts": comparison["missing_parts"],
        "parts": comparison["parts"],
        "alignment": align_info,
        # image ko text (data URL) bana diya taaki web page seedha dikha sake
        "image": to_data_url(annotated),
    }

    # alignment fail hua to user ko bata do ki result pe pura bharosa mat karo
    if not align_info["aligned"]:
        result["warning"] = ("Could not line up this photo with the reference. "
                             "Check it is the same board and camera position.")
    return result