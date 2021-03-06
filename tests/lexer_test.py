from unittest import TestCase
from typing import List
from cantte.token import Token, TokenType
from cantte.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.DIVISION, '/'),
            Token(TokenType.MULTIPLICATION, '*'),
            Token(TokenType.LESS_THAN, '<'),
            Token(TokenType.GREATER_THAN, '>'),
            Token(TokenType.NEGATION, '!'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source: str = '(){},;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assigment(self) -> None:
        source: str = 'let five = 5;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENTIFIER, 'five'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''
            let sum = func(x, y) {
                x + y;
            };
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENTIFIER, 'sum'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FUNCTION, 'func'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENTIFIER, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENTIFIER, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENTIFIER, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENTIFIER, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_function_call(self) -> None:
        source: str = 'let result = sum(dos, tres);'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENTIFIER, 'result'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENTIFIER, 'sum'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENTIFIER, 'dos'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENTIFIER, 'tres'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_control_statement(self) -> None:
        source: str = '''
            if (5 < 10) {
                return true;
            } else {
                return false;
            }
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'if'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LESS_THAN, '<'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.TRUE, 'true'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'else'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.FALSE, 'false'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:
        source: str = '''
            10 == 10;
            10 != 9;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(8):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10'),
            Token(TokenType.EQUAL, '=='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.INT, '10'),
            Token(TokenType.NOT_EQUAL, '!='),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_string(self) -> None:
        source: str = '''
            "foo";
            "This is a string";
            'Other string';
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(6):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, 'foo'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.STRING, 'This is a string'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.STRING, 'Other string'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)
