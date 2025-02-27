from connector_db import dbconfig
from exequte_queries import QueryHandler

def main():
    query_handler = QueryHandler(dbconfig)

    try:
        while True:
            print("\nВыберите действие:")
            print("1. Поиск фильма по ключевому слову")
            print("2. Поиск фильма по жанру и году")
            print("3. Показать популярные запросы")
            print("4. Выйти")
            choice = input("Введите номер команды: ")

            if choice == "1":
                keyword = input("Введите ключевое слово: ")
                results = query_handler.get_film_by_keyword(keyword)
                if results:
                    for row in results:
                        print(row)
                else:
                    print(f"По слову: '{keyword}' ничего не найдено")
            elif choice == "2":
                genre = input("Введите жанр: ")
                try:
                    year = int(input("Введите год: "))
                except ValueError:
                    print("Ошибка: Год должен быть числом!")
                    continue

                results = query_handler.get_film_by_janr_and_year(genre, year)
                if results:
                    for row in results:
                        print(row)
                else:
                    print("К сожилению ничего не найдено :(")
            elif choice == "3":
                popular_searches = query_handler.get_popular_searches()
                for query, count in popular_searches:
                    print(f"{query}: {count} раз(а)")
            elif choice == "4":
                print("Надеюсь вы нашли нужний фильм.\n      Процес завершен :(")
                break
            else:
                print("Некорректный ввод, попробуйте снова.")
    finally:
        query_handler.close()


if __name__ == "__main__":
    main()