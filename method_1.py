import utils
import ollama


def run_step(current_page_title, target_topic, target_keywords, links):
    link_titles = list(links.keys())

    # Step 1: Filter top 10 using SBERT
    candidates = utils.find_best_sbert_matches(link_titles, target_keywords, top_k=10)

    # Step 2: Ask Llama to pick the best one
    candidates_str = "\n".join([f"- {c}" for c in candidates])

    prompt = f"""
    Wikipedia Game. Current Page: "{current_page_title}". Target Goal: "{target_topic}".
    Select the single best link from the list below to get logically closer to the target.

    Candidates:
    {candidates_str}

    Reply ONLY with the exact link text. No explanations.
    """

    try:
        response = ollama.chat(model="llama3.1", messages=[{'role': 'user', 'content': prompt}])
        llm_choice = response['message']['content'].strip().replace('"', '').replace("'", "")

        # Validation
        for cand in candidates:
            if cand.lower() in llm_choice.lower():
                return cand
        return candidates[0]  # Fallback to SBERT #1
    except:
        return candidates[0]