import utils


def run_step(current_page_title, target_topic, target_keywords, links):
    link_titles = list(links.keys())

    # Select the mathematically closest link (Top 1)
    candidates = utils.find_best_sbert_matches(link_titles, target_keywords, top_k=1)

    if candidates:
        return candidates[0]
    else:
        return link_titles[0]  # Fallback