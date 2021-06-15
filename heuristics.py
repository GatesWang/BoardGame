from search import Node

def h1(node):
    # subtract number of pieces
    return len(node.agent_count) - len(node.advesary_count)

def h2(node):
    # our pieces minus their pieces
    answer = 0
    pieces = [1,2,3]
    for piece in pieces:
        answer += node.agent_count[piece] - node.advesary_count[piece]
    return answer

def h3(node):
    answer = 0
    pieces = [1,2,3]
    for piece in pieces:
        answer += h3_helper(piece, node.agent_count, node.advesary_count)
    return answer

def h3_helper(piece, agent, advesary):
    # higher is better for agent, lower is better for advesary
    #our pieces minus their pieces
    answer = agent[piece] - advesary[piece]
    # get what counters this
    counter = (piece-1)%3
    answer -= advesary[counter]
    # get what this counters
    counters = (piece+1)%3
    counter += advesary[counters]
    return answer
