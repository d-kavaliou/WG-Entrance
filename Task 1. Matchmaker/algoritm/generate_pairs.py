from collections import namedtuple

TeamRating = namedtuple('TeamRating', ['id', 'rating'])
TeamDiff = namedtuple('TeamDiff', ['diff', 'index'])


def generate_pairs(iterable, key):
    sorted_iterable = sorted(iterable, key=key)
    iter_len = len(sorted_iterable)

    # check whether the iterable is odd
    if iter_len % 2 == 1:
        # get the diffs of odd items and choose the max value
        team_rating_to_be_removed = max(_compute_odd_diffs(sorted_iterable), key=lambda item: item.diff)
        # the element with the biggest value should be left without pair
        sorted_iterable.pop(team_rating_to_be_removed.index)

    # generate pairs
    for index in range(0, iter_len - 1, 2):
        yield sorted_iterable[index], sorted_iterable[index + 1]


def _compute_odd_diffs(sorted_list):
    last_index = len(sorted_list) - 1

    # we have to consider the special cases
    # for first and last items, because they have only one nearby element
    penultimate_index = last_index - 1

    # diff for the first element
    yield TeamDiff(sorted_list[1].rating - sorted_list[0].rating, 0)

    # loop through the remaining items
    for index in range(1, penultimate_index):
        # check the diff only for odd items
        # in our case we skip the first item, therefore we compute diff for even elements
        if index % 2 == 0:
            yield TeamDiff((sorted_list[index + 1].rating - sorted_list[index].rating) +
                           (sorted_list[index].rating - sorted_list[index - 1].rating), index)

    # diff for the last element
    yield TeamDiff(sorted_list[last_index].rating - sorted_list[penultimate_index].rating, last_index)