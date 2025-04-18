from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

def recall_trainer(file_path):
    with open(file_path, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip() != ""]

    print("Tape chaque ligne de mémoire. Tu peux taper 'skip' pour passer à la ligne suivante, ou 'quit' pour arrêter.\n")

    bindings = KeyBindings()
    session = PromptSession(history=InMemoryHistory(), auto_suggest=AutoSuggestFromHistory(), key_bindings=bindings)

    @bindings.add('(')
    def _(event):
        event.app.current_buffer.insert_text('()')
        event.app.current_buffer.cursor_left()

    @bindings.add('[')
    def _(event):
        event.app.current_buffer.insert_text('[]')
        event.app.current_buffer.cursor_left()

    @bindings.add('{')
    def _(event):
        event.app.current_buffer.insert_text('{}')
        event.app.current_buffer.cursor_left()

    @bindings.add('"')
    def _(event):
        event.app.current_buffer.insert_text('""')
        event.app.current_buffer.cursor_left()

    @bindings.add("'")
    def _(event):
        event.app.current_buffer.insert_text("''")
        event.app.current_buffer.cursor_left()

    @bindings.add('backspace')
    def _(event):
        buf = event.app.current_buffer
        pos = buf.cursor_position
        if pos > 0:
            prev_char = buf.text[pos - 1]
            pair = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
            if prev_char in pair:
                next_pos = pos
                if next_pos < len(buf.text) and buf.text[next_pos] == pair[prev_char]:
                    buf.delete(count=1)  # Supprimer le caractère de fermeture
        buf.delete_before_cursor()

    for i, expected in enumerate(lines):
        hint_level = 0
        error_count = 0
        while True:
            user_input = session.prompt(f"Ligne {i+1} > ")
            # Auto-closing of common scopes
            pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
            for open_sym, close_sym in pairs.items():
                if user_input.count(open_sym) > user_input.count(close_sym):
                    user_input += close_sym * (user_input.count(open_sym) - user_input.count(close_sym))

            if user_input == 'quit':
                print("Fin de la session.")
                return
            if user_input == 'skip':
                print(f"⏭️  Skipped. La ligne correcte était : {expected}")
                break
            if user_input == expected.strip():
                print("✅ Correct !")
                break
            else:
                error_count += 1
                print("❌ Incorrect, réessaie.")
                if error_count >= 2:
                    hint_level = min(len(expected), hint_level + 5)
                    hint = expected[:hint_level] + ("…" if hint_level < len(expected) else "")
                    print(f"💡 Indice : {hint}")

    print("\n🎉 Bien joué ! Tu as terminé le fichier.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python recall_trainer.py <chemin_du_fichier>")
    else:
        recall_trainer(sys.argv[1])
