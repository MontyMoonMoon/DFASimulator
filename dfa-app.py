import streamlit as st
import base64
from PIL import Image

from visual_automata.fa.dfa import VisualDFA

r1 = "RegEx 1. (1+0)(1+0)*(11+00)(11+00)* (1+0)(0+1)(11*00*)((00)*+(11)*)(11+00)(11+00)*(1+0)*"
r2 = "RegEx 2. (aa+bb)(a+b)*(aba+bab+bbb+aaa)(ab+ba)*(bb+aa)(a+b)*(a*ba*ba*)(bab+bba+bbb+aba)(a+b)*"

# Use the full page 
st.set_page_config(layout="wide")
st.title("Deterministic Finite Automaton (DFA) Simulator with Push Down Automata & Context-Free Grammar")

# Divide page by columns of equal size
c1, c2, c3, c4 = st.columns(4)

with c1:    
    st.subheader("① Choose a Regular Expression")
    user_choice = st.selectbox("", [r1, r2])

with c2:
    st.subheader("② Context-Free Grammar ")

st.markdown("---")    
st.markdown("## DFA Simulation")

# Display chosen RegEx
st.text(user_choice)

if user_choice == r1:
  dfa = VisualDFA(
    states={'0', '1', '2', '3', '4', '5', '6', '7', '8'},
    input_symbols={"0", "1"},
    transitions={
        '0': {'0': '1', '1': '1'},
        '1': {'0': '2', '1': '3'},
        '2': {'0': '4', '1': '8'},  # '8' is a dead state
        '3': {'0': '8', '1': '4'},
        '4': {'0': '5', '1': '5'},
        '5': {'0': '6', '1': '6'},
        '6': {'0': '7', '1': '7'},
        '7': {'0': '7', '1': '7'},
        '8': {'0': '8', '1': '8'},  # trap/dead state
    },
    initial_state='0',
    final_states={'7'},
)


with c2:
        # Add CFG within an expander
        my_expander = st.expander("Expand", expanded=True)
        with my_expander:
            st.write("S -> ABCDAAEHCDB")
            st.write("A -> 1 | 0")
            st.write("B -> 1A | 0A | λ")
            st.write("C -> 11 | 00")
            st.write("D -> 11D | 00D | λ")
            st.write("E -> 1F0G")
            st.write("F -> 1F |  λ")
            st.write("G -> 0G|  λ")
            st.write("H -> I |  J")
            st.write("I -> 00I |  λ")
            st.write("J -> 11J | λ")

if user_choice == r2:
    dfa = VisualDFA(
    states={str(i) for i in range(14)},  # 0 through 13
    input_symbols={"a", "b"},
    transitions={
        
        '0': {'a': '1', 'b': '2'},
        '1': {'a': '3', 'b': '11'},  
        '2': {'b': '3', 'a': '11'},

   
        '3': {'a': '3', 'b': '3',  'a': '4', 'b': '7'},


        '4': {'a': '8', 'b': '5'},
        '5': {'a': '9', 'b': '12'},
        '7': {'a': '12', 'b': '6'},
        '6': {'a': '12', 'b': '9'},
        '8': {'a': '9', 'b': '12'},

        '9': {'a': '13', 'b': '10'},  
        '13': {'b': '9', 'a': '12'},  

   
        '10': {'a': '11', 'b': '12'},
        '11': {'a': '11', 'b': '11'},  

   
        '12': {'a': '12', 'b': '12'},
    },
    initial_state='0',
    final_states={'12'},
)


with c2:
        y_expander = st.expander("Expand", expanded=True)
        with y_expander:
            st.write("S -> ABCDABEGB")
            st.write("A -> aa | bb")
            st.write("B  -> aB | bB | λ")
            st.write("C -> aba | bab | bbb | aaa") 
            st.write("D -> abD | baD | λ")
            st.write("E -> FbFbFb")
            st.write("F -> aF |  λ")
            st.write("G -> bab | bba | bbb | aba")

# Load PDA images
if user_choice == r1:
    pda_image = Image.open(os.path.join("images", "PDA1.png"))
elif user_choice == r2:
    pda_image = Image.open(os.path.join("images", "PDA 2.png"))

# Limit the height of the image
aspect_ratio = pda_image.width / pda_image.height
new_height = min(pda_image.height, 500)
new_width = int(new_height * aspect_ratio)
pda_image_resized = pda_image.resize((new_width, new_height))

# Display PDA image
with c4:
    st.subheader("④ Pushdown Automaton (PDA)")
    st.image(pda_image_resized)

# String Checker and DFA Simulation code...

try:
    with c3:
        st.subheader("③  String Checker")
        string = st.text_input("Enter a String below to Simulate Automaton")
        test = st.button('Test')
           
    if test and not string:
        c3.write("You need to enter a string!")         
    elif user_choice == c1 or c2 and test:
        try: 
            checker = dfa.input_check(string)
            if "[Accepted]" in checker:
                result = "VALID ✅ "
                DFA = dfa.show_diagram(string)
            else:
                result = "INVALID ⭕ "
                DFA = dfa.show_diagram(string)
        except:
            result = "INVALID ⭕ "
        c3.write("**" + result + "**")
                  
    # ------------------------------------------------------------
    # Option B to Display DFA Simulation
    st.write(DFA)

    # ------------------------------------------------------------
    # Option A to Display DFA Simulation using base64
    
    # Reformat and save DFA as .svg
    DFA.format = "svg"
    DFA.render("automaton")

    # Open the saved .svg file from local directory
    s = open("automaton.svg", "r")
    lines = s.readlines()
    DFA_Final = ''.join(lines)

    # Display inputted string
    st.write("Transition graph for string **" + string + "**.")

    def render_svg(svg):
        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" alt="DFA" style="width:100%%; height:auto;">' % b64
        st.write(html, unsafe_allow_html=True)

    render_svg(DFA_Final)

except Exception as e:
    st.empty()
    print('Finished...')
    print(e)
