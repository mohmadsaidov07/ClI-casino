def dice_pic(num) -> str:
    if num == 1:
        return ("___________\n"
                "|         |\n"
                "|    *    |\n"
                "|         |\n"
                "-----------\n"
                )
    if num == 2:
        return ("___________\n"
                "|       * |\n"
                "|         |\n"
                "| *       |\n"
                "-----------\n"
                )
    if num == 3:
        return ("___________\n"
                "|       * |\n"
                "|    *    |\n"
                "| *       |\n"
                "-----------\n"
                )
    if num == 4:
        return ("___________\n"
                "| *     * |\n"
                "|         |\n"
                "| *     * |\n"
                "-----------\n"
                )
    if num == 5:
        return ("___________\n"
                "| *     * |\n"
                "|    *    |\n"
                "| *     * |\n"
                "-----------\n"
                )
    if num == 6:
        return ("-----------\n"
                "| *     * |\n"
                "| *     * |\n"
                "| *     * |\n"
                "-----------\n"
                )
    
if __name__ == "__main__":
    print(dice_pic(6))