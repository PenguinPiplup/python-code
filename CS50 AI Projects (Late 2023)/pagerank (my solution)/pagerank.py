import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Sort pages according to whether they are linked
    prob_dist = {}
    linked_count = 0
    links_count = len(corpus)
    for website in corpus:
        if website in corpus[page]:
            prob_dist[website] = "Linked"
            linked_count += 1
        else:
            prob_dist[website] = "Unlinked"

    # Calculate the probability for visiting each website
    if linked_count > 0:
        linked_prob = damping_factor / linked_count
        unlinked_prob = (1 - damping_factor) / links_count
    else:
        unlinked_prob = 1 / links_count

    # Update dictionary with probability of visiting each website
    for web in prob_dist:
        if prob_dist[web] == "Linked":
            prob_dist[web] = linked_prob + unlinked_prob
        else:
            prob_dist[web] = unlinked_prob

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise dictionary containing estimated PageRank (number of samples divided by n) of each website
    page_rank = {}
    for web in corpus:
        page_rank[web] = 0

    # Randomly choose a page for the first sample and update page_rank
    current_page = random.choice(list(corpus))
    page_rank[current_page] = 1 / n

    # Collect another n - 1 samples
    for sample in range(1, n):
        # Choose a page at random
        tmpdict = transition_model(corpus, current_page, damping_factor)
        random_float = random.random()
        for page in tmpdict:
            random_float -= tmpdict[page]
            if random_float < 0:
                current_page = page
                break

        # Update page_rank
        page_rank[current_page] += 1 / n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise dictionary containing estimated PageRank of each website
    page_rank = {}
    links_count = len(corpus)
    for web in corpus:
        page_rank[web] = 1 / links_count

    # Constant for first part of the formula
    formula_constant = (1 - damping_factor) / links_count

    # Iterate until no pagerank changes by more than 0.001
    while True:
        # Counter to store number of pages whose pagerank changes by more than 0.001
        counter = len(page_rank)

        # Iterate over all the pages
        for page in page_rank:
            
            # Calculate second part of formula
            sumsum = 0
            for webpage in page_rank:
                if len(corpus[webpage]) == 0:
                    sumsum += page_rank[webpage] / links_count
                elif page in corpus[webpage]:
                    sumsum += page_rank[webpage] / len(corpus[webpage])

            # Calculate new page rank using first and second part of formula
            updated_rank = formula_constant + damping_factor * sumsum

            # Update counter (if applicable)
            if abs(page_rank[page] - updated_rank) < 0.001:
                counter -= 1

            # Update page rank
            page_rank[page] = updated_rank

        # If no pagerank changes by more than 0.001, return page_rank
        if counter == 0:
            return page_rank


if __name__ == "__main__":
    main()
